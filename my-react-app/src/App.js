import React from 'react';
import { ApolloProvider } from '@apollo/react-hooks';
import ApolloClient from 'apollo-boost';
import { useQuery, useMutation } from '@apollo/react-hooks';
import { gql } from 'graphql-tag';

const client = new ApolloClient({
    uri: 'http://localhost:8080/graphql/',
  });

  ReactDOM.render(
    <ApolloProvider client={client}>
      <App />
    </ApolloProvider>,
    document.getElementById('root')
  );
  



const GET_ALL_TASKS = gql`
  query {
    all_tasks {
      id
      title
      description
      # Include other fields you need
    }
  }
`;

const CREATE_TASK = gql`
  mutation CreateTask($title: String!, $description: String!, $priority: String!, $category_id: Int!, $username: String!) {
    create_task(title: $title, description: $description, priority: $priority, category_id: $category_id, username: $username) {
      task {
        id
        title
        description
        # Include other fields you need
      }
    }
  }
`;

function App() {
  const { loading, error, data } = useQuery(GET_ALL_TASKS);
  const [createTask] = useMutation(CREATE_TASK);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      {/* Render tasks here */}
    </div>
  );
}

export default App;
