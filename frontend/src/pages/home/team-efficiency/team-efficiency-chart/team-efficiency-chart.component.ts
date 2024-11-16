import { CommonModule } from '@angular/common';
import { Component, Input, ViewChild } from '@angular/core';

import {
  ApexAxisChartSeries,
  ApexTitleSubtitle,
  ApexChart,
  ApexXAxis,
  ChartComponent,
  NgApexchartsModule,
} from 'ng-apexcharts';

export type ChartOptions = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  title: ApexTitleSubtitle;
  xaxis: ApexXAxis;
};

export interface Config {
  categories: string[];
  data: number[];
}

@Component({
  selector: 'app-team-efficiency-chart',
  standalone: true,
  imports: [CommonModule, NgApexchartsModule],
  templateUrl: './team-efficiency-chart.component.html',
  styleUrl: './team-efficiency-chart.component.scss',
})
export class TeamEfficiencyChartComponent {
  @ViewChild('chart') chart!: ChartComponent;

  public chartOptions!: Partial<ChartOptions>;

  @Input({ required: true })
  public get config(): Config {
    return this._config;
  }
  public set config(value: Config) {
    this._config = value;
    this.chartOptions = {
      series: [
        {
          name: 'Series 1',
          data: value.data,
        },
      ],
      chart: {
        height: 350,
        type: 'radar',
      },
      xaxis: {
        categories: value.categories,
      },
    };
  }
  private _config!: Config;

  constructor() {}
}
