import gql from "graphql-tag";

export const GET_PROGRAM_WORKOUTS = gql`
  query($programId: ID!) {
    programWorkouts(programId: $programId) {
      id
      name
      orderInProgram
    }
  } 
`;
