import { Component } from '@angular/core';
import { ChartCardComponent } from './chart-card/chart-card.component';
import { TaskCycleAnalysisComponent } from './task-cycle-analysis/task-cycle-analysis.component';
import { LoadIndicatorComponent } from './load-indicator/load-indicator.component';
import { TeamEfficiencyComponent } from './team-efficiency/team-efficiency.component';
import { HomeFiltersComponent } from './home-filters/home-filters.component';
import { MlApiService } from '../../services/ml-api.service';
import { SprintsService } from '../../services/sprints.service';
import { SprintMetricsGroup } from '../../models/sprint.model';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    ChartCardComponent,
    TaskCycleAnalysisComponent,
    LoadIndicatorComponent,
    TeamEfficiencyComponent,
    HomeFiltersComponent,
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
})
export class HomeComponent {
  res?: SprintMetricsGroup;

  allSprints?: { sprintName: string; result: SprintMetricsGroup[] }[];

  dates?: Date[];

  get notComplete() {
    if (!this.res) return 0;
    return (
      this.res.baseMetricsNumeric.created + this.res.baseMetricsNumeric.ongoing
    );
  }

  get ongoing() {
    if (!this.res) return 0;
    return this.res?.baseMetricsNumeric.ongoing;
  }

  get created() {
    if (!this.res) return 0;
    return this.res?.baseMetricsNumeric.created;
  }

  get success() {
    if (!this.res) return 0;
    return this.res?.baseMetricsNumeric.success;
  }

  get fail() {
    if (!this.res) return 0;
    return this.res?.baseMetricsNumeric.fail;
  }

  get health() {
    if (!this.res) return 0;
    return this.res?.health.healthValue;
  }

  constructor(private _sprintsService: SprintsService) {
    const today = new Date();
    const prevMonth = new Date();
    prevMonth.setMonth(today.getMonth() - 1);
    this._sprintsService
      .getAllSprintMetrics(prevMonth, today)
      .subscribe((res) => {
        this.res = res;
      });
    this._sprintsService
      .getAllSprintMetricsOverall(prevMonth, today)
      .subscribe((res) => {
        debugger;
        this.allSprints = res.sprints;
        this.dates = res.intervals.map(interval => new Date(interval));
      });
  }
}
