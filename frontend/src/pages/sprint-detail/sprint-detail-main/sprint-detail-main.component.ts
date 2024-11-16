import { Component } from '@angular/core';
import { ChartCardComponent } from "../../home/chart-card/chart-card.component";
import { SprintEstimationComponent } from "./sprint-estimation/sprint-estimation.component";
import { TaskStagesComponent } from "./task-stages/task-stages.component";
import { SprintCardComponent } from "./sprint-card/sprint-card.component";

@Component({
  selector: 'app-sprint-detail-main',
  standalone: true,
  imports: [ChartCardComponent, SprintEstimationComponent, TaskStagesComponent, SprintCardComponent],
  templateUrl: './sprint-detail-main.component.html',
  styleUrl: './sprint-detail-main.component.scss'
})
export class SprintDetailMainComponent {

}
