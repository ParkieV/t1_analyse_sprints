import { Component, Input } from '@angular/core';
import {
  ApexNonAxisChartSeries,
  ApexResponsive,
  ApexChart,
  NgApexchartsModule,
  ApexLegend,
} from 'ng-apexcharts';

export type ChartOptions = {
  series: ApexNonAxisChartSeries;
  chart: ApexChart;
  responsive: ApexResponsive[];
  labels: string[];
  colors: string[];
  legend: ApexLegend;
  dataLabels: any;
  plotOptions: any;
};

export interface Config {
  categories: string[];
  data: number[];
  colors: string[];
}

@Component({
  selector: 'app-task-stages-chart',
  standalone: true,
  imports: [NgApexchartsModule],
  templateUrl: './task-stages-chart.component.html',
  styleUrl: './task-stages-chart.component.scss',
})
export class TaskStagesChartComponent {
  total!: number;

  public chartOptions!: Partial<ChartOptions>;

  @Input({ required: true })
  public get config(): Config {
    return this._config;
  }
  public set config(value: Config) {
    this.total = value.data.reduce((a, b) => a + b);
    this._config = value;
    this.chartOptions = {
      series: value.data,
      chart: {
        type: 'donut',
        height: 220,
        width: 220,
      },
      labels: value.categories,
      colors: value.colors,
      legend: {
        show: false,
      },
      dataLabels: {
        enabled: false,
      },
      responsive: [
        {
          breakpoint: 480,
          options: {
            chart: {
              width: 220,
              height: 220,
            },
            legend: {
              position: 'bottom',
            },
          },
        },
      ],
    };
  }
  private _config!: Config;

  constructor() {}
}
