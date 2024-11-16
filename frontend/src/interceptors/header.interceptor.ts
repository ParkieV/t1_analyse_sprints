import {
  HttpEvent,
  HttpHandler,
  HttpHeaders,
  HttpInterceptor,
  HttpRequest,
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

import { Injectable } from '@angular/core';
import { AuthService } from '../services/auth.service';

@Injectable()
export class HeaderInterceptor implements HttpInterceptor {
  constructor(private readonly _authService: AuthService) {}

  intercept(
    req: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    let headers: HttpHeaders = req.headers;
    if (!headers.has('Content-Type')) {
      headers = headers.set('Content-Type', 'application/json');
    } else if (headers.get('Content-Type') === '') {
      headers = headers.delete('Content-Type');
    }
    if (!headers.has('Accept')) {
      headers = headers.set('Accept', 'application/json');
    }

    if (this._authService.isLogged) {
      headers = headers.set(
        'Authorization',
        `Bearer ${this._authService.jwtToken}`
      );
    }

    const clone = req.clone({
      headers,
    });

    return next.handle(clone).pipe(
      map((v) => {
        return v;
      }),
      catchError((error) => {
        if (error.status !== 401) {
          return throwError(() => error);
        }
        this._authService.signOut();
        return throwError(() => error);
      })
    );
  }
}
