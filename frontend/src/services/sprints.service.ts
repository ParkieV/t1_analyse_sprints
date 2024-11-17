import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import {
  combineLatest,
  combineLatestAll,
  concatAll,
  concatMap,
  map,
  mergeMap,
  Observable,
  switchMap,
  tap,
  toArray,
} from 'rxjs';
import { Sprint, SprintMetricsGroup } from '../models/sprint.model';
import { MlApiService } from './ml-api.service';

function padZeros(v: number): string {
  const s = v.toString();
  if (s.length === 1) {
    return '0' + s;
  }
  return s;
}

function getDateString(date: Date): string {
  return `${date.getFullYear()}-${padZeros(date.getMonth() + 1)}-${padZeros(
    date.getDate()
  )} ${date.toLocaleTimeString()}`;
}

@Injectable({
  providedIn: 'root',
})
export class SprintsService {
  constructor(
    private readonly _apiService: ApiService,
    private readonly _mlApiService: MlApiService
  ) {}

  getSprints(): Observable<Sprint[]> {
    const url = 'data/sprints';
    return this._apiService
      .get<Sprint[]>(url, {
        params: {
          page_size: '2',
          page_number: '1',
        },
      })
      .pipe(
        mergeMap((res) => {
          return res.map((sprint) => {
            // debugger;
            return this.getSprintMetrics(
              sprint.sprintName,
              new Date(sprint.sprintStartDate),
              new Date(sprint.sprintEndDate)
            ).pipe(
              map((metrics) => {
                sprint.metrics = metrics;
                return sprint;
              })
            );
          });
        }, 6),
        concatAll(),
        toArray()
      );
  }

  getSprint(id: string) {
    const url = `data/sprints/${id}`;
    return this._apiService.get(url);
  }

  getSprintMetricsRight(
    sprintName: string,
    dateTo: Date
  ): Observable<SprintMetricsGroup> {
    const url = 'base_metrics_interval';
    const dateToString = getDateString(dateTo);
    return this._mlApiService.get(url, {
      params: {
        sprint_name: sprintName,
        time: dateToString,
      },
    });
  }

  getSprintMetrics(
    sprintName: string,
    dateFrom: Date,
    dateTo: Date
  ): Observable<SprintMetricsGroup> {
    const url = 'base_metrics_interval';
    // debugger;
    const dateFromString = getDateString(dateFrom);
    const dateToString = getDateString(dateTo);
    return this._mlApiService.get(url, {
      params: {
        sprint_name: sprintName,
        time_left: dateFromString,
        time_right: dateToString,
      },
    });
  }

  getAllSprintMetrics(
    dateFrom: Date,
    dateTo: Date
  ): Observable<SprintMetricsGroup> {
    const url = 'base_metrics_all_sprints_interval';
    // debugger;
    const dateFromString = getDateString(dateFrom);
    const dateToString = getDateString(dateTo);
    return this._mlApiService.get(url, {
      params: {
        time_left: dateFromString,
        time_right: dateToString,
      },
    });
  }
}
