
import {
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'

import './App.css';
import Form from './components/Form';
const queryClient = new QueryClient()

const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="flex justify-center align-center">
        <Form />
      </div>
    </QueryClientProvider>
  );
}

export default App;