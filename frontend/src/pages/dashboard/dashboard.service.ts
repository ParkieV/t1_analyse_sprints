import { ChangeDetectorRef, Injectable } from '@angular/core';
import { Container } from './dashboard.component';

@Injectable()
export class DashboardService {
  hostContainer!: Container;

  isEditing: boolean = false;

  constructor(private _cdr: ChangeDetectorRef) {
    if (!this.load()) {
      this.init();
    }
  }

  init() {
    this.hostContainer = {
      elements: [
        {
          type: 'widget',
          component: '',
          flex: 1,
        },
      ],
      flex: 1,
      position: 'row',
    };
  }

  edit() {
    this.isEditing = true;
  }

  save() {
    this.isEditing = false;
    localStorage.setItem(
      'customDashboard',
      JSON.stringify(this.hostContainer)
    );
  }

  load() {
    const dashboardRaw = localStorage.getItem('customDashboard');
    if (dashboardRaw) {
      this.hostContainer = JSON.parse(dashboardRaw);
      return true;
    }
    return false;
  }

  clear() {
    localStorage.removeItem('customDashboard');
    this.init();
  }
}
