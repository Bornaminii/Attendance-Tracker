import authReducer from "../src/store/authSlice";

test("auth state starts idle", () => {
  const state = authReducer(undefined, { type: "unknown" });
  expect(state.status).toBe("idle");
});
