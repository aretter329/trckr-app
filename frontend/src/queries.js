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
