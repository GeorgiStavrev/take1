class QueueStorage {
    constructor(queueName) {
        this.name = queueName
        this.dataKey = `qdata-${queueName}`
    }

    load(queue) {
        if (queue.name === this.name) {
            const data = localStorage.getItem(this.dataKey)
            if (data != null) {
                const deserialized = JSON.parse(data);
                queue.items = deserialized.items
                queue.frontIndex = deserialized.frontIndex
                queue.backIndex = deserialized.backIndex
            }
        }
    }

    store(queue) {
        if (queue.name === this.name) {
            localStorage.setItem(this.dataKey, JSON.stringify(queue))
        }
    }
}

class Queue {
    constructor(name) {
        this.name = name
        this.items = {}
        this.frontIndex = 0
        this.backIndex = 0
        console.log("Create queue with name " + this.name)
        this.storage = new QueueStorage(this.name)
        this.storage.load(this)
    }
    pushRight(item) {
        this.items[this.backIndex] = item
        this.backIndex++
        this.storage.store(this)
        return item + ' inserted at the tail'
    }
    pushLeft(item) {
        this.frontIndex--
        this.items[this.frontIndex] = item
        this.storage.store(this)
        return item + ' inserted at the head'
    }
    popLeft() {
        const item = this.items[this.frontIndex]
        delete this.items[this.frontIndex]
        this.frontIndex++
        this.storage.store(this)
        return item
    }
    peek() {
        return this.items[this.frontIndex]
    }
    size() {
        return Object.keys(this.items).length;
    }
    get printQueue() {
        return this.items;
    }
}

function makeid(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
}
        
async function postEvents(tracker, events) {
    await fetch("http://localhost:8000/api/v1/track", {
        method: "POST",
        body: JSON.stringify({
            user_id: tracker.userId,
            events: events,
            properties: []
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8",
          "Authorization": `Bearer ${tracker.accessToken}`
        }
    });
}
        
async function flush(tracker, timeout) {
    var toFlush = [];
    while (toFlush.length < 100 && tracker.events.size() > 0) {
        const event = tracker.events.popLeft()
        if (event != null) {
            toFlush.push(event)
        }        
    }
    if (tracker.tokenExpiration < new Date()) {
        await tracker.refresh()
    }
    try {
        if (toFlush.length > 0 && tracker.verbose) {
            console.log(`Flushing ${toFlush.length} events. Timeout is ${timeout}`);
        }
        await postEvents(tracker, toFlush);
    } catch (error) {
        for (var i = toFlush.length - 1; i >= 0; i--) {
            tracker.events.pushLeft(toFlush[i])
        }
        if (toFlush.length > 0 && tracker.verbose) {
            console.log(`Flush failed.`);
        }
    }
    setTimeout(async () => { await flush(tracker, timeout) }, timeout);
}

async function authenticate(username, password) {
    var response = await fetch("http://localhost:8000/api/token", {
        method: "POST",
        body: JSON.stringify({
            username: username,
            password: password
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
    });
    return await response.json()
}

async function refreshAuth(refreshToken) {
    var response = await fetch("http://localhost:8000/api/token/refresh", {
        method: "POST",
        body: JSON.stringify({
            refresh: refreshToken,
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
    });
    return await response.json()
}

function parseJwt (token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

const DEFAULT_TIMEOUT_VALUE = 1000
const MAX_INIT_ATTEMPTS = 3
const MAX_REFRESH_ATTEMPTS = 3
class Tracker {
    constructor(timeout=DEFAULT_TIMEOUT_VALUE) {
        this.events = new Queue("take1Tracker");
        this.properties = [];
        this.userId = `anon${makeid(10)}`;
        this.verbose = false;
        this.timeout = timeout
        if (timeout === undefined) {
            timeout = DEFAULT_TIMEOUT_VALUE
        }
        console.log(`Create Tracker. Timeout is ${timeout}`)
    }
    async init(clientId, apiKey, attempt) {
        try {
            if (attempt === undefined || attempt == null) {
                attempt = 0
            }
            var response = await authenticate(clientId, apiKey)
            this.accessToken = response.access
            this.refreshToken = response.refresh
            this.tokenExpiration = new Date(1000 * parseJwt(this.accessToken)["exp"])
        } catch(err) {
            if (attempt < MAX_INIT_ATTEMPTS) {
                setTimeout(() => this.init(clientId, apiKey, attempt+1), 3000);
            }
        }
    }
    async refresh(attempt) {
        try {
            if (attempt === undefined || attempt == null) {
                attempt = 0
            }
            var response = await refreshAuth(this.refreshToken);
            this.accessToken = response.access
            this.refreshToken = response.refresh
            this.tokenExpiration = new Date(1000 * parseJwt(this.accessToken)["exp"])
        } catch(err) {
            if (attempt < MAX_REFRESH_ATTEMPTS) {
                setTimeout(() => this.refresh(attempt+1), 3000);
            }
        }
    }
    identify(userId) {
        this.userId = userId;
    }
    startTracking() {
        if (this.verbose) {
            console.log(`Start tracking for client_id ${this.clientId} and user_id ${this.userId}`);
        }
        window.addEventListener("load", (pageLoadEvent) => {
            this.track("pageView", [{ "url": pageLoadEvent.target.URL }])
        });
    
        setTimeout(async () => { await flush(this, this.timeout) }, this.timeout);
    }
    track(event, properties) {
        var propArray = [];
        properties.forEach((key, idx) => {
            const property = properties[idx];
            Object.keys(property).forEach((name, _) => {
                propArray.push({
                    name: name,
                    value: property[name]
                });
            });

        });
        this.events.pushRight({
            event: event,
            created_at: (new Date()).toISOString(),
            properties: propArray
        })
    }
}

export default Tracker;
