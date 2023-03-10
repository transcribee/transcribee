import { Observable } from 'lib0/observable';
import * as Y from 'yjs';

enum MessageSyncType {
  Change = 1,
  ChangeBacklogComplete = 2,
}
export class WebsocketProvider extends Observable<'update' | 'initalSyncComplete'> {
  ws!: WebSocket;
  url: string;
  yDoc: Y.Doc;

  constructor(url: string, yDoc: Y.Doc) {
    super();

    this.url = url;
    this.yDoc = yDoc;

    this.connectWebsocket();
  }

  connectWebsocket() {
    this.ws = new WebSocket(this.url);

    this.ws.addEventListener('open', (e) => {
      console.debug('[ws] Connected', e);
    });

    this.yDoc.on('update', (update, origin) => {
      if (origin !== this) {
        if (this.ws.readyState === this.ws.OPEN) {
          this.ws.send(update);
        }

        this.emit('update', [update]);
      }
    });

    this.on('update', (update: Uint8Array) => {
      Y.applyUpdate(this.yDoc, update, this);
    });

    this.ws.addEventListener('message', async (event: MessageEvent) => {
      const msg_data = new Uint8Array(await event.data.arrayBuffer());
      const msg_type = msg_data[0];
      const msg = msg_data.slice(1);
      if (msg_type === MessageSyncType.Change) {
        this.emit('update', [msg]);
      } else if (msg_type === MessageSyncType.ChangeBacklogComplete) {
        this.emit('initalSyncComplete', []);
        console.log('All changes synced');
      }
    });

    this.ws.addEventListener('close', () => setTimeout(() => this.connectWebsocket(), 1000));
  }
}
