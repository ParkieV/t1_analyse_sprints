import { CommonModule } from '@angular/common';
import {
  Component,
  EventEmitter,
  HostBinding,
  Input,
  Output,
} from '@angular/core';
import { Container, Widget } from '../dashboard.component';
import { MatMenuModule } from '@angular/material/menu';
import { DashboardWidgetComponent } from '../dashboard-widget/dashboard-widget.component';
import { DashboardService } from '../dashboard.service';

@Component({
  selector: 'app-dashboard-container',
  standalone: true,
  imports: [CommonModule, MatMenuModule, DashboardWidgetComponent],
  templateUrl: './dashboard-container.component.html',
  styleUrl: './dashboard-container.component.scss',
})
export class DashboardContainerComponent {
  @Input() container!: Container;

  @Output() createContainer = new EventEmitter<'column' | 'row'>();

  @HostBinding('class')
  get position() {
    return this.container.position;
  }

  get isEditing() {
    return this._dashboardService.isEditing;
  }

  get hostContainer() {
    return this._dashboardService.hostContainer;
  }

  constructor(private readonly _dashboardService: DashboardService) {}

  ngOnInit() {
    // debugger;
    // if (!this.container.elements.length) {
    //   this.addWidget();
    // }
  }

  onAddContainer(newContainerPosition: 'column' | 'row') {
    this.addContainer(newContainerPosition);
  }

  addOutsideContainer(newContainerPosition: 'column' | 'row') {
    this.createContainer.next(newContainerPosition);
  }

  addContainer(newContainerPosition: 'column' | 'row', index?: number) {
    // debugger;
    // const prevElements = this.container.elements;
    if (newContainerPosition === this.container.position) {
      this.addWidget();
      // this.createContainer.next(newContainerPosition);
      return;
    }

    if (index === undefined) index = this.container.elements.length - 1;
    const widget = this.container.elements[index];
    const newParent: { type: 'container' } & Container = {
      type: 'container',
      elements: [
        widget,
        {
          type: 'widget',
          component: '',
          flex: 1,
        },
      ],
      flex: widget.flex,
      position: newContainerPosition,
    };
    widget.flex = 1;
    this.container.elements[index] = newParent;

    // this.container.elements.push(newParent);

    // this.container.elements = [newParent];
    // this.container.position = newContainerPosition;
  }

  addWidget(widget?: Widget) {
    this.container.elements.push({
      type: 'widget',
      component: '',
      flex: 1,
      ...widget,
    });
  }
}
