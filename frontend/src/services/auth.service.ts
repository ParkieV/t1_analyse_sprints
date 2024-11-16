import { Injectable } from '@angular/core';
import { User } from '../models/user.company';
import { delay, Observable, of, tap } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  isLogged: boolean = false;

  authorizedUser?: User;

  constructor() {
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
    return of()
      .pipe(delay(1000))
      .pipe(
        tap(() => {
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
