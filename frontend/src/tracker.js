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
    pushLeftMany(items) {
        for (var i = 0; i < items.length; i++) {
            this.pushLeft(items[i])
        }
    }
    popLeft() {
        const item = this.items[this.frontIndex]
        delete this.items[this.frontIndex]
        this.frontIndex++
        this.storage.store(this)
        return item
    }
    popLeftMany(count) {
        var result = []
        while (result.length < 100 && this.size() > 0) {
            const item = this.popLeft()
            if (item != null) {
                result.push(item)
            }        
        }
        return result
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
        
async function postEvents(tracker, events, properties) {
    await fetch("http://localhost:8000/api/v1/track", {
        method: "POST",
        body: JSON.stringify({
            user_id: tracker.userId,
            events: events,
            properties: properties
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8",
          "Authorization": `Bearer ${tracker.accessToken}`
        }
    });
}
        
async function flush(tracker, timeout) {
    var eventsToFlush = tracker.events.popLeftMany(100);
    var propertiesToFlush = tracker.properties.popLeftMany(100);
    if (tracker.tokenExpiration < new Date()) {
        await tracker.refresh()
    }
    if (eventsToFlush.length == 0 && propertiesToFlush.length == 0) {
        setTimeout(async () => { await flush(tracker, timeout) }, timeout);
        return
    }
    
    try {
        if (eventsToFlush.length > 0 && tracker.verbose) {
            console.log(`Flushing ${eventsToFlush.length} events and ${propertiesToFlush.length} properties. Timeout is ${timeout}`);
        }
        await postEvents(tracker, eventsToFlush, propertiesToFlush);
    } catch (error) {
        tracker.events.pushLeftMany(eventsToFlush.reverse());
        tracker.events.pushLeftMany(propertiesToFlush.reverse());
        if (eventsToFlush.length > 0 && tracker.verbose) {
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
        this.events = new Queue("take1Events");
        this.properties = new Queue("take1Properties");
        this.userId = `anon${makeid(10)}`;
        this.verbose = false;
        this.timeout = timeout
        if (timeout === undefined) {
            timeout = DEFAULT_TIMEOUT_VALUE
        }
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
    setProperty(name, value) {
        this.properties.pushRight({
            "name": name,
            "value": value
        })
    }
}

export default Tracker;
