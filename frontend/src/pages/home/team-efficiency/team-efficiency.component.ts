import { Component } from '@angular/core';
import { TeamEfficiencyChartComponent } from "./team-efficiency-chart/team-efficiency-chart.component";

@Component({
  selector: 'app-team-efficiency',
  standalone: true,
  imports: [TeamEfficiencyChartComponent],
  templateUrl: './team-efficiency.component.html',
  styleUrl: './team-efficiency.component.scss',
})
export class TeamEfficiencyComponent {
  title: string = 'Backend';

  subtitle: string = 'Самая эффективная команда';

  config = {
    categories: [
      'Backend',
      'Frontend',
      'Менеджмент',
      'Аналитика',
      'Финансы',
      'Тестирование',
      'Маркетинг',
      'Дизайн',
    ],
    data: [
      7,
      5,
      4,
      5,
      2,
      5,
      3,
      4,
    ]
  };
}
