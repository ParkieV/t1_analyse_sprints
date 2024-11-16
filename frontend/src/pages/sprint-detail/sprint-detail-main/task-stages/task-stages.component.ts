import { Component } from '@angular/core';
import { TaskStagesChartComponent } from './task-stages-chart/task-stages-chart.component';
import { CHART_COLORS } from '../../../../models/chart-colors';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-task-stages',
  standalone: true,
  imports: [CommonModule, TaskStagesChartComponent],
  templateUrl: './task-stages.component.html',
  styleUrl: './task-stages.component.scss',
})
export class TaskStagesComponent {
  get options(): {
    name: string;
    value: number;
    color: string;
    percent: number;
  }[] {
    const total = this.config.data.reduce((prev, acc = 0) => prev + acc);
    const result = []
    for (let i = 0; i < this.config.categories.length; i++) {
      result.push({
        name: this.config.categories[i],
        value: this.config.data[i],
        color: this.config.colors[i],
        percent: this.config.data[i] / total * 100,
      })
    }
    return result;
  }
  
  config = {
    categories: [
      'К выполнению',
      'В работе',
      'Выполнено'
    ],
    data: [7, 9, 15],
    colors: CHART_COLORS,
  };
}
