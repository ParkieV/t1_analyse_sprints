import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { TranslatePipe } from '@ngx-translate/core';

@Component({
  selector: 'app-sprints-table',
  standalone: true,
  imports: [CommonModule, RouterModule, MatTableModule, TranslatePipe],
  templateUrl: './sprints-table.component.html',
  styleUrl: './sprints-table.component.scss',
})
export class SprintsTableComponent {
  tableColumns = [
    'name',
    'status',
    'progress',
    'project',
    'lastChanges',
    'more',
  ];

  dataSource = new MatTableDataSource<any>();
}
