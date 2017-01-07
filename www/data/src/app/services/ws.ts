import { Injectable } from '@angular/core';

import { Observable } from 'rxjs/Observable';
import { Subscription } from 'rxjs/Subscription';
import { Subject } from 'rxjs/Subject';

import { BASE_HOST } from './constants';

let reconnectingwebsocket = require('reconnectingwebsocket');

@Injectable()
export class WsService {
  public connection: any;
  public rawStream$ = new Subject<any>();

  private _baseUrl: string;
  private _receivers: any;
  private _heartbeat: Subscription;
  private _failSendTimer: Subscription;
  private _failSendBuffer = [];
  private _failSendRetrying = false;

  constructor() {
    this.connect();
    this._receivers = {
      pong: (data) => {
        console.log('pong', data);
      },
      debug: (data) => {
        console.log('websocket debug pingback');
        console.log(data);
      }
    };
  }

  retryFailed() {
    for (let i in this._failSendBuffer) {
      if (this._send(this._failSendBuffer[i])) {
        this._failSendBuffer.splice(Number(i), 1);
      }
    }
    if (this._failSendBuffer.length === 0) this._failSendTimer.unsubscribe();
  }

  failSent(content) {
    /*
      If we pass 100 items, there are something really wrong.
      We don't want to fill up the memory, so for now, just try from time
      to time to resend.
      Heartbeats are not saved because it will be ~50 per day, all doing
      the same thing. Just let them trigger a retryFailed()
    */
    if (this._failSendBuffer.length <= 100 && content.action !== 'heartbeat') {
      this._failSendBuffer.push(content);
    }

    /*
    We dont want to retry failed messages forever, but sometimes, we could
    have failed because of many reasons. Example that someone tried to send
    a message before the websocket connection was up and ready..
    */
    if (this._failSendRetrying || this._failSendBuffer.length === 0) return;
    this._failSendRetrying = true;
    this._failSendTimer = Observable
      .interval(1000)
      .take(10)
      .finally(() => { this._failSendRetrying = false; })
      .subscribe((x) => this.retryFailed());

  }

  isConnected() {
    return this.connection.readyState === 1;
  }

  connect() {
    let protocol: string = location.protocol === 'http:' ? 'ws:' : 'wss:';

    this._baseUrl = protocol + '//' + BASE_HOST + '/_/ws/';
    this.connection = new reconnectingwebsocket(this._baseUrl, null, { debug: false });

    this.connection.onopen = () => {
      /*
      The serverside of our websocket framework might drop group memberships
      after a while. This is by design. A heartbeat re-subscribes to our current
      groups, and keep them "fresh".
      */
      if (!this._heartbeat) {
        this._heartbeat = Observable.timer(0, 1000 * 60 * 30).subscribe(() => this.heartbeat());
      }
    };

    this.connection.onmessage = (event) => {
      let content;
      try {
        content = JSON.parse(event.data);
      } catch (err) {
        console.log('Unable to parse data for even', err);
        console.log(event);
        return false;
      };

      let action = content.action;
      let data = content.data || {};

      this.rawStream$.next({ action: action, data: data });
      if (action in this._receivers) {
        this._receivers[action](data);
      }
    };
  }

  on(action: string, func: Function) {
    this._receivers[action] = func;
  }


  _send(content) {
    try {
      this.connection.send(JSON.stringify(content));
      return true;
    } catch (err) {
      console.log('Unable to send websocket message', err);
      return false;
    };
  }

  send(action: string, data?) {
    let content = {
      action: action || 'ping',
      data: data || {}
    };
    if (!this._send(content)) {
      this.failSent(content);
    }
  }

  heartbeat() {
    this.send('heartbeat');
    if (!this._failSendRetrying) {
      this.failSent({ action: 'heartbeat' });
    }
  }

  subscribe(group, opts = {}) {
    let data = {
      group: group,
      scope: opts['scope'] || 'pub',
      save: opts['save'] || false,
      tag: opts['tag'] || '',
      unsubscribe_tag_first: opts['unsubscribe_tag_first'] || false
    };
    this.send('subscribe', data);
  }

  unsubscribe(opts = {}) {
    let data = {
      group: opts['group'] || '',
      scope: opts['scope'] || 'pub',
      save: opts['save'] || false,
      tag: opts['tag'] || ''
    };
    this.send('unsubscribe', data);
  }

  receive(action, func) {
    this._receivers[action] = func;
  }

  open() {
    this.connection.open();
  }

  close(code, reason) {
    this.connection.close(code, reason);
  }

  refresh() {
    this.connection.refresh();
  }
}
