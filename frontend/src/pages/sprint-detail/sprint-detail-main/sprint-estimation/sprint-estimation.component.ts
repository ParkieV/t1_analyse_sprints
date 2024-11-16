import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { SprintEstimationChartComponent } from "./sprint-estimation-chart/sprint-estimation-chart.component";

@Component({
  selector: 'app-sprint-estimation',
  standalone: true,
  imports: [CommonModule, SprintEstimationChartComponent],
  templateUrl: './sprint-estimation.component.html',
  styleUrl: './sprint-estimation.component.scss',
})
export class SprintEstimationComponent {
  estimationDate: Date = new Date();

  comment: string = 'на 3 дня раньше запланированного';
}
