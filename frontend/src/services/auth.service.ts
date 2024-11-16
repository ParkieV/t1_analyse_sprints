import { Injectable } from '@angular/core';
import { User } from '../models/user.company';
import { delay, Observable, of, tap } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ApiService } from './api.service';

interface AuthResponse {
  accessToken: string;
}

const UNIVERSAL_USER: User = {
  id: 1,
  fullName: 'Елизавета Боткина',
  photo:
    'https://static.vecteezy.com/system/resources/thumbnails/030/798/360/small_2x/beautiful-asian-girl-wearing-over-size-hoodie-in-casual-style-ai-generative-photo.jpg',
};

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  isLogged: boolean = false;

  authorizedUser?: User;

  jwtToken?: string;

  constructor(private _apiService: ApiService) {
    this._checkIsAuthorized();
  }

  private _checkIsAuthorized(): void {
    const token = sessionStorage.getItem('jwt');
    if (token) {
      this.isLogged = true;
      this.authorizedUser = UNIVERSAL_USER;
      this.jwtToken = token;
    } else {
      this.isLogged = false;
      this.authorizedUser = undefined;
      this.jwtToken = undefined;
      sessionStorage.removeItem('jwt');
    }
  }

  public signIn(username: string, password: string): Observable<AuthResponse> {
    let headers = new HttpHeaders();
  headers = headers.set('Content-Type', 'application/x-www-form-urlencoded');
    const dataFormStringified = `grant_type=password&username=${username}&password=${password}`;
    return this._apiService
      .post<AuthResponse>('auth/token', dataFormStringified, {
        headers,
      })
      .pipe(
        tap((res) => {
          debugger;
          this.jwtToken = res.accessToken;
          this.isLogged = true;
          this.authorizedUser = UNIVERSAL_USER;
          sessionStorage.setItem('jwt', this.jwtToken);
        })
      );
  }

  public signOut(): Observable<null> {
    return of(null)
      .pipe(delay(300))
      .pipe(
        tap(() => {
          this.isLogged = false;
          this.authorizedUser = undefined;
          this.jwtToken = undefined;
          sessionStorage.removeItem('jwt');
        })
      );
  }
}
