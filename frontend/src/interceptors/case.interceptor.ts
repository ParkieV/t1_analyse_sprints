import {
  HttpEvent,
  HttpHandler,
  HttpHeaders,
  HttpInterceptor,
  HttpRequest,
  HttpResponse,
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class CaseInterceptor implements HttpInterceptor {
  constructor() {}

  private snakeToCamel = (str: string): string =>
    str.replace(/([_]\w)/g, (g) => g[1].toUpperCase());

  private camelToSnake = (str: string): string =>
    str.replace(/([A-Z])/g, (group) => '_' + group.toLowerCase());

  private isObject = function (o: any): o is Record<string, object> {
    return o === Object(o) && !Array.isArray(o) && typeof o !== 'function';
  };

  private keysToCamel = (o: object): object => {
    if (Array.isArray(o)) {
      return o.map((i) => {
        return this.keysToCamel(i);
      });
    } else if (this.isObject(o)) {
      const n: Record<string, object> = {};

      Object.keys(o).forEach((k) => {
        n[this.snakeToCamel(k)] = this.keysToCamel(o[k]);
      });

      return n;
    }

    return o;
  };

  private keysToSnake = (o: object): object => {
    if (this.isObject(o)) {
      const n: Record<string, object> = {};

      Object.keys(o).forEach((k) => {
        n[this.camelToSnake(k)] = this.keysToSnake(o[k]);
      });

      return n;
    } else if (Array.isArray(o)) {
      return o.map((i) => {
        return this.keysToSnake(i);
      });
    }

    return o;
  };

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(req).pipe(
      map((event: HttpEvent<any>) => {
        if (event instanceof HttpResponse) {
          if (
            event.body &&
            (<HttpHeaders>event.headers).has('Content-Type') &&
            (<HttpHeaders>event.headers).get('Content-Type') === 'application/json'
          ) {
            return event.clone({ body: this.keysToCamel(event.body) });
          }
          return event;
        }
        return event;
      }),
    );
  }
}
