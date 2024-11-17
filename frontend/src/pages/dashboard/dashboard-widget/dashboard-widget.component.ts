import { CommonModule } from '@angular/common';
import {
  ChangeDetectorRef,
  Component,
  ComponentFactoryResolver,
  Input,
  Type,
  ViewChild,
} from '@angular/core';
import { Container, Widget } from '../dashboard.component';
import { ViewHostDirective } from './view-host.directive';
import { MatMenuModule } from '@angular/material/menu';
import { LoadIndicatorComponent } from '../../home/load-indicator/load-indicator.component';
import { TeamEfficiencyComponent } from '../../home/team-efficiency/team-efficiency.component';
import { TaskCycleAnalysisComponent } from '../../home/task-cycle-analysis/task-cycle-analysis.component';
import { DashboardService } from '../dashboard.service';

type WidgetComponent = any;

const widgets: { [key: string]: Type<WidgetComponent> } = {
  loadIndicator: LoadIndicatorComponent,
  teamEfficiency: TeamEfficiencyComponent,
  taskCycleAnalysis: TaskCycleAnalysisComponent,
};

@Component({
  selector: 'app-dashboard-widget',
  standalone: true,
  imports: [CommonModule, ViewHostDirective, MatMenuModule],
  templateUrl: './dashboard-widget.component.html',
  styleUrl: './dashboard-widget.component.scss',
})
export class DashboardWidgetComponent {
  @ViewChild(ViewHostDirective)
  public get hostRef(): ViewHostDirective {
    return this._hostRef;
  }
  public set hostRef(value: ViewHostDirective) {
    this._hostRef = value;
    debugger;
    if (this.activeComponent) this._renderComponent(this.activeComponent);
  }
  private _hostRef!: ViewHostDirective;

  @Input() canResize: boolean = true;

  @Input() canResizeContainer: boolean = true;

  @Input() container!: Container;

  @Input()
  public get widget(): Widget {
    return this._widget;
  }

  public set widget(value: Widget) {
    this._widget = value;
    if (value.component) {
      this.selectWidget(value.component);
    }
  }

  private _widget!: Widget;

  widgets: {
    key: string;
    name: string;
  }[] = [
    {
      key: 'loadIndicator',
      name: 'Load Indicator',
    },
    {
      key: 'teamEfficiency',
      name: 'TeamEfficiency',
    },
    {
      key: 'taskCycleAnalysis',
      name: 'taskCycleAnalysis',
    },
  ];

  get isEditing() {
    return this._dashboardService.isEditing;
  }

  activeComponent?: Type<Widget>;

  constructor(
    private readonly _cdr: ChangeDetectorRef,
    private readonly _dashboardService: DashboardService
  ) {}

  setFlex(flex: number) {
    this.widget.flex = flex;
  }

  setContainerFlex(flex: number) {
    this.container.flex = flex;
  }

  selectWidget(name: string) {
    const widget = widgets[name];
    if (!widget) {
      throw new Error('Undefined widget');
    }
    this.widget.component = name;
    this._renderComponent(widget);
  }

  private _renderComponent(component: Type<WidgetComponent>) {
    this.activeComponent = component;
    
    if (!this.hostRef) return;
    const viewContainerRef = this.hostRef.viewContainerRef;
    viewContainerRef.clear();
    viewContainerRef.createComponent(component);
    this._cdr.detectChanges();
  }
}
