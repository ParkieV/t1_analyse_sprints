import { Component } from '@angular/core';
import { DashboardFiltersComponent } from './dashboard-filters/dashboard-filters.component';
import { DashboardContainerComponent } from "./dashboard-container/dashboard-container.component";
import { DashboardService } from './dashboard.service';

export interface Widget {
  component: string;
  flex: number;
}

export interface Container {
  position: 'column' | 'row';
  elements: (
    | ({
        type: 'widget';
      } & Widget)
    | ({ type: 'container' } & Container)
  )[];
  flex: number;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [DashboardFiltersComponent, DashboardContainerComponent],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
  providers: [DashboardService]
})
export class DashboardComponent {
  get parentContainer() {
    return this._dashboardService.hostContainer;
  }

  constructor(private readonly _dashboardService: DashboardService) {}
}
