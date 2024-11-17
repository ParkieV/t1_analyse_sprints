import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SprintsService } from '../../../services/sprints.service';
import { CommonModule } from '@angular/common';
import { SprintDetailService } from '../sprint-detail.service';
import { SprintKanbanComponent } from "./sprint-kanban/sprint-kanban.component";

@Component({
  selector: 'app-sprint-detail-tasks',
  standalone: true,
  imports: [CommonModule, SprintKanbanComponent],
  templateUrl: './sprint-detail-tasks.component.html',
  styleUrl: './sprint-detail-tasks.component.scss'
})
export class SprintDetailTasksComponent {
  get tasks() {
    return this._sprintDetailService.sprint.entities;
  }
  
  isLoading: boolean = false;

  constructor(private readonly _sprintDetailService: SprintDetailService, private readonly _activatedRoute: ActivatedRoute) {
    this._sprintDetailService.loads.subscribe((isLoading) => {
      this.isLoading = isLoading;
    })
  }
}
