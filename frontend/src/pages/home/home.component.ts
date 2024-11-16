import { Component } from '@angular/core';
import { ChartCardComponent } from "./chart-card/chart-card.component";
import { TaskCycleAnalysisComponent } from './task-cycle-analysis/task-cycle-analysis.component';
import { LoadIndicatorComponent } from './load-indicator/load-indicator.component';
import { TeamEfficiencyComponent } from "./team-efficiency/team-efficiency.component";
import { HomeFiltersComponent } from './home-filters/home-filters.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [ChartCardComponent, TaskCycleAnalysisComponent, LoadIndicatorComponent, TeamEfficiencyComponent, HomeFiltersComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {

}
