import { Component } from '@angular/core';
import { LoadIndicatorScaleComponent } from "./load-indicator-scale/load-indicator-scale.component";

@Component({
  selector: 'app-load-indicator',
  standalone: true,
  imports: [LoadIndicatorScaleComponent],
  templateUrl: './load-indicator.component.html',
  styleUrl: './load-indicator.component.scss'
})
export class LoadIndicatorComponent {

  value: number = 70;

  title: string = 'Оптимально';

  subtitle: string = 'Сотрудники загружены оптимально';

}
