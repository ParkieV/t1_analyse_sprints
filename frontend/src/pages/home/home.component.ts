import { Component } from '@angular/core';
import { ChartCardComponent } from "./chart-card/chart-card.component";

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [ChartCardComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {

}
