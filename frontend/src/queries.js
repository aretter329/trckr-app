import gql from "graphql-tag";

export const GET_DAYS_BY_PROGRAM = gql`
  query($programId: ID!) {
    daysByProgram(programId: $programId) {
      id
      name
      orderInProgram
    }
  }
`;

export const GET_PROGRAM_WORKOUTS = gql`
  query($programId: ID!) {
    programWorkouts(programId: $programId) {
      id
      name
      orderInProgram
    }
  } 
`;
