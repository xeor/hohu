import { Injectable } from '@angular/core';
import { Http, Headers, Response } from '@angular/http';
import { Observable } from 'rxjs/Rx';

import { CookieService } from 'angular2-cookie/core';

import { BASE_URL } from './constants';

@Injectable()
export class ApiService {
  constructor(private _http: Http, private _cookie: CookieService) {}

  _get_headers() {
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('X-CSRFToken', this._cookie.get('csrftoken'));
    return {
      headers: headers,
      withCredentials: true
    };
  }

  _get_full_url(url) {
    if (url.startsWith('http://') || url.startsWith('https://')) {
      // If we are using the next parameter from eg paginated resources
      return url;
    } else {
      return `${BASE_URL}/_/api/${url}`;
    }
  }

  get(url): Observable<Response> {
    let fullUrl = this._get_full_url(url);
    return this._http.get(fullUrl, this._get_headers());
  }

  post(url, data): Observable<Response> {
    let fullUrl = this._get_full_url(url);
    return this._http.post(fullUrl, JSON.stringify(data), this._get_headers());
  }

  put(url, data): Observable<Response> {
    let fullUrl = this._get_full_url(url);
    return this._http.put(fullUrl, JSON.stringify(data), this._get_headers());
  }
}
