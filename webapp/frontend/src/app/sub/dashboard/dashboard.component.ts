import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  btcusdChange!: string;
  aaplChange!: string;
  uberChange!: string;
  dsaChange!: string;
  isLoading: boolean = true;


  query = '';
  data: any[] = [];
  tabLoading = true;
  constructor(private http: HttpClient) { }

  ngOnInit() {
    // Make requests to Alpha Vantage API for each asset
    this.http.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=BTCUSD&apikey=AORMSJJL3MBAG177').subscribe((data: any) => {
      if (data.hasOwnProperty('Global Quote') && data['Global Quote'].hasOwnProperty('10. change percent')) {
        this.btcusdChange = data['Global Quote']['10. change percent'];
      }
    });
    this.http.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=AORMSJJL3MBAG177').subscribe((data: any) => {
      if (data.hasOwnProperty('Global Quote') && data['Global Quote'].hasOwnProperty('10. change percent')) {
        this.aaplChange = data['Global Quote']['10. change percent'];
      }
    });
    this.http.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=UBER&apikey=AORMSJJL3MBAG177').subscribe((data: any) => {
      if (data.hasOwnProperty('Global Quote') && data['Global Quote'].hasOwnProperty('10. change percent')) {
        this.uberChange = data['Global Quote']['10. change percent'];
      }
    });
    this.http.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=DSY.PA&apikey=AORMSJJL3MBAG177').subscribe((data: any) => {
      if (data.hasOwnProperty('Global Quote') && data['Global Quote'].hasOwnProperty('10. change percent')) {
        this.dsaChange = data['Global Quote']['10. change percent'];
      }
    });
  }

  formatChange(change: string): string {
    let nbchange = this.parseFloat(change)
    const sign = Math.sign(nbchange);
    const absChange = Math.abs(nbchange);
    const formattedChange = parseFloat(absChange.toFixed(2)).toLocaleString();

    return (sign >= 0 ? '+' : '-') + formattedChange + '%';
  }

  parseFloat(stringValue: string): number {
    return parseFloat(stringValue);
  }

  onSubmit() {
    this.tabLoading = true;
    this.http.get<any[]>(`http://127.0.0.1:5001/api/v1/predictions/news/AAPL`).subscribe(data => {
      this.tabLoading = false;
      this.data = data;
    });
  }


}
