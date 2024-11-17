import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { keysToSnake } from './stringUtils';

export interface HttpOptions {
  headers?: HttpHeaders;
  observe?: 'body';
  params?:
    | HttpParams
    | {
        [param: string]: string | string[];
      };
  reportProgress?: boolean;
  responseType?: 'json';
  withCredentials?: boolean;
  body?: any | null;
}

@Injectable({
  providedIn: 'root',
})
export class MlApiService {
  constructor(private http: HttpClient) {}

  private formatErrors(error: any) {
    return throwError(error);
  }

  get<T = any>(path: string, options?: HttpOptions): Observable<T> {
    return this.http
      .get<T>(`${MlApiService.apiUrl}${path}`, options)
      .pipe(catchError(this.formatErrors));
  }

  put<T = any>(
    path: string,
    body: Object,
    options?: HttpOptions
  ): Observable<T> {
    body = this.intercept(body, options);
    return this.http
      .put<T>(`${MlApiService.apiUrl}${path}`, body, options)
      .pipe(catchError(this.formatErrors));
  }

  patch<T = any>(
    path: string,
    body: Object,
    options?: HttpOptions
  ): Observable<T> {
    body = this.intercept(body, options);
    return this.http
      .patch<T>(`${MlApiService.apiUrl}${path}`, body, options)
      .pipe(catchError(this.formatErrors));
  }

  post<T = any>(
    path: string,
    body: Object,
    options?: HttpOptions
  ): Observable<T> {
    body = this.intercept(body, options);
    return this.http
      .post<T>(`${MlApiService.apiUrl}${path}`, body, options)
      .pipe(catchError(this.formatErrors));
  }

  delete<T = any>(path: string, options?: HttpOptions): Observable<T> {
    return this.http
      .delete<T>(`${MlApiService.apiUrl}${path}`, options)
      .pipe(catchError(this.formatErrors));
  }

  intercept(body: any, options?: HttpOptions) {
    if (
      !options ||
      !options.headers ||
      !options.headers.has('Content-Type') ||
      options.headers.get('Content-Type') === 'application/json'
    ) {
      return keysToSnake(body); 
    }
    return body;
  }

  static get apiUrl() {
    return 'http://localhost/api_ml/';
  }
}
