import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-load-indicator-scale',
  standalone: true,
  imports: [],
  templateUrl: './load-indicator-scale.component.html',
  styleUrl: './load-indicator-scale.component.scss'
})
export class LoadIndicatorScaleComponent {

  x: number = 0;

  /** Значение от 0 до 100 */
  @Input({ required: true })
  public get value(): number {
    return this._value;
  }
  public set value(value: number) {
    this._value = value;
    this.x = (value / 100) * 496;
  }
  private _value!: number;
}
