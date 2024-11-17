import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { RouterModule } from '@angular/router';
import { TranslatePipe } from '@ngx-translate/core';
import { Employee } from '../../../models/employee.model';
import { StaffService } from '../../../services/staff.service';

@Component({
  selector: 'app-staff-table',
  standalone: true,
  imports: [CommonModule, RouterModule, MatTableModule, TranslatePipe],
  templateUrl: './staff-table.component.html',
  styleUrl: './staff-table.component.scss',
})
export class StaffTableComponent {
  tableColumns = [
    'name',
    'sprint',
    'area',
    'lastChanges',
    'more',
  ];

  dataSource = new MatTableDataSource<Employee>();

  constructor(private _staffService: StaffService) {
    this._staffService.getEmployees().subscribe((res) => {
      this.dataSource.data = res;
    });
  }
}
