import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { Observable } from 'rxjs';
import { Sprint } from '../models/sprint.model';

@Injectable({
  providedIn: 'root',
})
export class SprintsService {
  constructor(private readonly _apiService: ApiService) {}

  getSprints(): Observable<Sprint[]> {
    const url = 'data/sprints';
    return this._apiService.get(url, {
      params: {
        page_size: '15',
        page_number: '1',
      },
    });
  }

  getSprint(id: string) {
    const url = `data/sprints/${id}`;
    return this._apiService.get(url);
  }
}
