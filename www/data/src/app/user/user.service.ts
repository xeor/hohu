import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import { Observable } from 'rxjs/Observable';

import { BASE_URL } from '../services/constants';
import { RequestBase } from '../services/request-base';

@Injectable()
export class UserService extends RequestBase {
  constructor(public http: Http) {
    super(http);
  }

  logout(): Observable<string> {
    return this.http.get(`${BASE_URL}/logout`, this.optionsNoPre)
      .map(res => res.text());
  }
}
