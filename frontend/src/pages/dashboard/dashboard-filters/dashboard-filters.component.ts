import { Component } from '@angular/core';
import { DateSelectorComponent } from '../../../components/date-selector/date-selector.component';
import { CommonModule } from '@angular/common';
import { DashboardService } from '../dashboard.service';

@Component({
  selector: 'app-dashboard-filters',
  standalone: true,
  imports: [CommonModule, DateSelectorComponent],
  templateUrl: './dashboard-filters.component.html',
  styleUrl: './dashboard-filters.component.scss',
})
export class DashboardFiltersComponent {
  get isEditing() {
    return this._dashboardService.isEditing;
  }

  constructor(private readonly _dashboardService: DashboardService) {}

  save() {
    this._dashboardService.save();
  }

  edit() {
    this._dashboardService.edit();
  }

  clear() {
    this._dashboardService.clear();
  }
}
