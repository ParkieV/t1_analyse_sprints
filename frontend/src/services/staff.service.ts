import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { Employee } from '../models/employee.model';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class StaffService {
  constructor(private readonly _apiService: ApiService) {}

  getEmployees(): Observable<Employee[]> {
    const url = 'data/employees';
    // , {
    //   params: {
    //     page_size: '15',
    //     page_number: '1',
    //   },
    // }
    return this._apiService.get(url);
  }

  getEmployee(id: string) {
    const url = `data/employees/${id}`;
    return this._apiService.get(url);
  }
}
