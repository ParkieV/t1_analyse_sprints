import { Injectable } from '@angular/core';
import { User } from '../models/user.company';
import { delay, Observable, of, tap } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  isLogged: boolean = false;

  authorizedUser?: User;

  constructor(private _apiService: ApiService) {
    this._checkIsAuthorized();
  }

  private _checkIsAuthorized(): void {
    const token = sessionStorage.getItem('jwt');
    if (token) {
      this.isLogged = true;
      this.authorizedUser = JSON.parse(token);
    } else {
      this.isLogged = false;
      this.authorizedUser = undefined;
    }
  }

  public signIn(username: string, password: string): Observable<void> {
    return this._apiService
      .post('auth/token', {
        username: username,
        password: password,
      })
      .pipe(
        tap((res) => {
          debugger;
          this.isLogged = true;
          this.authorizedUser = {
            id: 1,
            fullName: 'Доброе утро',
          };
          sessionStorage.setItem('jwt', JSON.stringify(this.authorizedUser));
        })
      );
  }

  public signOut(): Observable<void> {
    return of()
      .pipe(delay(1000))
      .pipe(
        tap(() => {
          this.isLogged = false;
          this.authorizedUser = undefined;
          sessionStorage.removeItem('jwt');
        })
      );
  }
}
