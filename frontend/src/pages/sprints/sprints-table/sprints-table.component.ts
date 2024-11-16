import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { TranslatePipe } from '@ngx-translate/core';
import { SprintsService } from '../../../services/sprints.service';
import { Sprint } from '../../../models/sprint.model';

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

  dataSource = new MatTableDataSource<Sprint>();

  constructor(private _sprintService: SprintsService) {
    this._sprintService.getSprints().subscribe((res) => {
      this.dataSource.data = res;
    })
  }
} 
