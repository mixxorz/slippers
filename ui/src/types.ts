export type PropError = {
    error: "invalid" | "missing" | "extra";
    name: string;
    expected?: string;
    actual?: string;
};

export type SlippersError = {
    tag_name: string;
    template_name: string;
    lineno: number;
    errors: PropError[];
};
