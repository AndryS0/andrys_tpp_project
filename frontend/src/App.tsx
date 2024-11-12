// src/App.tsx
import React from 'react';
import './App.css';
import Calculator from './components/Calculator';
import {QueryClient, QueryClientProvider} from "react-query";
import PlanetsComponent from "./components/PlanetsComponent";
import SatellitesComponent from "./components/SatellitesComponent";
import StarsComponent from "./components/StarsComponent";

const queryClient = new QueryClient();

const App: React.FC = () => {
  return (

      <QueryClientProvider client={queryClient}>
          <div className="app">
              <h1>Space Management System</h1>
              <PlanetsComponent />
              <StarsComponent />
              <SatellitesComponent />
          </div>
          <div className="App">
              <Calculator />
          </div>
      </QueryClientProvider>
  );
};

export default App;
