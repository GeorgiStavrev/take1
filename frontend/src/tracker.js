class Queue {
    constructor() {
        this.items = {}
        this.frontIndex = 0
        this.backIndex = 0
    }
    enqueue(item) {
        this.items[this.backIndex] = item
        this.backIndex++
        return item + ' inserted'
    }
    dequeue() {
        const item = this.items[this.frontIndex]
        delete this.items[this.frontIndex]
        this.frontIndex++
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
        
function postEvents(tracker, events) {
    fetch("http://localhost:8000/api/v1/track", {
        method: "POST",
        body: JSON.stringify({
            client_id: tracker.clientId,
            user_id: tracker.userId,
            events: events,
            properties: []
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
    });
}
        
function flush(tracker) {
    var toFlush = [];
    while (toFlush.length < 100 && tracker.events.size() > 0) {
        toFlush.push(tracker.events.dequeue())
    }
    postEvents(tracker, toFlush);
    if (toFlush.length > 0 && tracker.verbose) {
        console.log(`Flushing ${toFlush.length} events.`);
    }
    setTimeout(() => { flush(tracker) }, 1000);
}

class Tracker {
    constructor(clientId) {
        this.events = new Queue();
        this.properties = [];
        this.clientId = clientId;
        this.userId = `anon${makeid(10)}`;
        this.verbose = false;
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
    
        setTimeout(() => { flush(this) }, 1000);
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
        this.events.enqueue({
            event: event,
            created_at: (new Date()).toISOString(),
            properties: propArray
        })
    }
}

export default Tracker;
