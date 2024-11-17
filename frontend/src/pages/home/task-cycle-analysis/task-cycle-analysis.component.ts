import { CommonModule } from '@angular/common';
import { dataSeries } from './data-series';
import { Component, Input } from '@angular/core';
import { TaskCycleAnalysisChartComponent } from './task-cycle-analysis-chart/task-cycle-analysis-chart.component';
import { TaskCycleAnalysisOptionComponent } from './task-cycle-analysis-option/task-cycle-analysis-option.component';
import { CHART_COLORS } from '../../../models/chart-colors';
import { SprintMetricsGroup } from '../../../models/sprint.model';

interface Option {
  title: string;
  color: string;
  dataSeries: any;
}

@Component({
  selector: 'app-task-cycle-analysis',
  standalone: true,
  imports: [
    CommonModule,
    TaskCycleAnalysisChartComponent,
    TaskCycleAnalysisOptionComponent,
  ],
  templateUrl: './task-cycle-analysis.component.html',
  styleUrl: './task-cycle-analysis.component.scss',
})
export class TaskCycleAnalysisComponent {
  @Input()
  dates!: Date[];

  @Input() set allSprints(
    value: { sprintName: string; result: SprintMetricsGroup[] }[]
  ) {
    debugger;
    setTimeout(() => {
      let i = 0;
      this.options = value.map((sprint) => {
        const dataSeries = [];
        for (let j = 0; j < sprint.result.length; j++) {
          dataSeries.push({
            date: this.dates[j],
            value: sprint.result[j].health.healthValue,
          });
        }
        return {
          title: sprint.sprintName,
          color: CHART_COLORS[i++],
          dataSeries: dataSeries,
        };
      });
      this.activeOption = this.options[0];
      debugger;
    });
  }

  title: string = 'Здоровье';

  subtitle: string = 'Спринты за последний месяц';

  options?: Option[];

  activeOption!: Option;

  ngOnInit() {}
}
