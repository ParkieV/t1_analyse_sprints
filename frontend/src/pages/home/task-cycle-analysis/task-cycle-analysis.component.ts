import { CommonModule } from '@angular/common';
import { dataSeries } from './data-series';
import { Component } from '@angular/core';
import { TaskCycleAnalysisChartComponent } from './task-cycle-analysis-chart/task-cycle-analysis-chart.component';
import { TaskCycleAnalysisOptionComponent } from './task-cycle-analysis-option/task-cycle-analysis-option.component';

const COLORS = ['#2CB28F', '#7FA6D2', '#4A13C3'];

interface Option {
  title: string;
  color: string;
  dataSeries: any;
}

@Component({
  selector: 'app-task-cycle-analysis',
  standalone: true,
  imports: [CommonModule, TaskCycleAnalysisChartComponent, TaskCycleAnalysisOptionComponent],
  templateUrl: './task-cycle-analysis.component.html',
  styleUrl: './task-cycle-analysis.component.scss',
})
export class TaskCycleAnalysisComponent {

  title: string = '8 дней';

  subtitle: string = 'Среднее время потраченное на задачу';

  options: Option[] = [
    {
      title: 'К выполнению',
      color: COLORS[0],
      dataSeries: dataSeries.slice(),
    },
    {
      title: 'В работе',
      color: COLORS[1],
      dataSeries: dataSeries.slice(),
    },
    {
      title: 'Сделано',
      color: COLORS[2],
      dataSeries: dataSeries.slice(),
    },
  ];

  activeOption!: Option;

  ngOnInit() {
    this.activeOption = this.options[0];
  }
}
