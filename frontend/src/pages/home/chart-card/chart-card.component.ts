import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { NgApexchartsModule } from 'ng-apexcharts';

@Component({
  selector: 'app-chart-card',
  standalone: true,
  imports: [NgApexchartsModule, CommonModule],
  templateUrl: './chart-card.component.html',
  styleUrl: './chart-card.component.scss',
})
export class ChartCardComponent {
  @Input({ required: true }) title!: string;

  @Input({ required: true }) value!: number;

  @Input({ required: true }) change!: number;
}
