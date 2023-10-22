import axios from "axios"
import { BalanceSheetFormData } from "../components/Form"

const BASE_URL: string = "http://localhost:8000";

export const fetchBalanceSheet = async (payload: BalanceSheetFormData) => await axios.post(`${BASE_URL}/balance_sheet/`, payload)
export const applyForLoan = async (payload: BalanceSheetFormData) => await axios.post(`${BASE_URL}/apply/`, payload)