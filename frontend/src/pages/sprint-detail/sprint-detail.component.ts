import { Component } from '@angular/core';
import { SprintHeaderComponent } from "./sprint-header/sprint-header.component";
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { SprintDetailService } from './sprint-detail.service';

@Component({
  selector: 'app-sprint-detail',
  standalone: true,
  imports: [CommonModule, RouterModule, SprintHeaderComponent],
  templateUrl: './sprint-detail.component.html',
  styleUrl: './sprint-detail.component.scss'
})
export class SprintDetailComponent {
  constructor(private _activatedRoute: ActivatedRoute, private _sprintDetailService: SprintDetailService) {
    this._activatedRoute.paramMap.subscribe((res) => {
      this._sprintDetailService.sprintId = res.get('sprintId')!;
      this._sprintDetailService.getSprint();
    })
  }
}
