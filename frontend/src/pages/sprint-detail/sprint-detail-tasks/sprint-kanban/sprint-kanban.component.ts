import { Component } from '@angular/core';
import { SprintDetailService } from '../../sprint-detail.service';

@Component({
  selector: 'app-sprint-kanban',
  standalone: true,
  imports: [],
  templateUrl: './sprint-kanban.component.html',
  styleUrl: './sprint-kanban.component.scss'
})
export class SprintKanbanComponent {

  get kanban() {
    return this._sprintDetailService.kanban;
  }

  isLoading: boolean = false

  constructor(private readonly _sprintDetailService: SprintDetailService) {
    this._sprintDetailService.loads.subscribe((isLoading) => {
      this.isLoading = isLoading;
    })
  }
}
