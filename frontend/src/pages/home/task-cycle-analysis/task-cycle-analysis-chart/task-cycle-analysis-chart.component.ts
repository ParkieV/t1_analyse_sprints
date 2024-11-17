import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import {
  ApexAxisChartSeries,
  ApexChart,
  ApexDataLabels,
  ApexFill,
  ApexMarkers,
  ApexTitleSubtitle,
  ApexTooltip,
  ApexXAxis,
  ApexYAxis,
  NgApexchartsModule,
} from 'ng-apexcharts';

@Component({
  selector: 'app-task-cycle-analysis-chart',
  standalone: true,
  imports: [CommonModule, NgApexchartsModule],
  templateUrl: './task-cycle-analysis-chart.component.html',
  styleUrl: './task-cycle-analysis-chart.component.scss',
})
export class TaskCycleAnalysisChartComponent {
  public series!: ApexAxisChartSeries;
  public chart!: ApexChart;
  public dataLabels!: ApexDataLabels;
  public markers!: ApexMarkers;
  public title!: ApexTitleSubtitle;
  public fill!: ApexFill;
  public yaxis!: ApexYAxis;
  public xaxis!: ApexXAxis;
  public tooltip!: ApexTooltip;

  @Input({ required: true}) color!: string;
  
  @Input({ required: true })
  public get dataSeries(): { date: string; value: number; }[] {
    return this._dataSeries;
  }
  public set dataSeries(value: { date: string; value: number; }[]) {
    this._dataSeries = value;
    this.initChartData();
  }
  private _dataSeries!: { date: string; value: number; }[];

  constructor() {
  }

  ngOnInit() {
    // this.initChartData();
  }

  public initChartData(): void {
    let ts2 = 1484418600000;
    let dates = [];
    for (let i = 0; i < this.dataSeries.length; i++) {
      ts2 = ts2 + 86400000;
      dates.push([new Date(this.dataSeries[i].date).getTime(), this.dataSeries[i].value]);
    }

    debugger;

    this.series = [
      {
        name: 'XYZ MOTORS',
        data: dates,
      },
    ];
    this.chart = {
      type: 'area',
      stacked: false,
      height: 350,
      zoom: {
        type: 'x',
        enabled: true,
        autoScaleYaxis: true,
      },
      toolbar: {
        autoSelected: 'zoom',
      },
    };
    this.dataLabels = {
      enabled: false,
    };
    this.markers = {
      size: 0,
    };
    this.title = {
      // text: 'Stock Price Movement',
      align: 'left',
    };
    this.fill = {
      colors: [this.color]
      // type: 'fill',
      // gradient: {
      //   shadeIntensity: 1,
      //   inverseColors: false,
      //   opacityFrom: 0.5,
      //   opacityTo: 0,
      //   stops: [0, 90, 100],
      // },
    };
    this.yaxis = {
      labels: {
        formatter: function (val) {
          return (val).toFixed(0);
        },
      },
      // title: {
      //   text: 'Price',
      // },
    };
    this.xaxis = {
      type: 'datetime',
    };
    this.tooltip = {
      shared: false,
      y: {
        formatter: function (val) {
          return (val).toFixed(0);
        },
      },
    };
  }
}
