import React, { useState, useEffect } from "react";

declare global {
    interface Window {
        slippersPropErrors: [SlippersError];
    }
}

type PropError = {
    error: "invalid" | "missing" | "extra";
    name: string;
    expected?: string;
    actual?: string;
};

type SlippersError = {
    tag_name: string;
    template_name: string;
    lineno: number;
    errors: PropError[];
};

const Var = ({ children }: { children: React.ReactNode }) => (
    <span className="text-indigo-400 font-mono">{children}</span>
);

const Tag = ({ children }: { children: React.ReactNode }) => (
    <span className="text-orange-400 font-mono">{children}</span>
);

const Type = ({ children }: { children: React.ReactNode }) => (
    <span className="text-teal-400 font-mono">{children}</span>
);

const ErrorBox = ({
    error: { tag_name, template_name, lineno, errors },
}: {
    error: SlippersError;
}) => (
    <div>
        <p>{tag_name}</p>
        <p className="text-zinc-400">
            {template_name}:{lineno}
        </p>
        <ul className="mt-4 pl-4">
            {errors.map((error, i) => (
                <li key={i}>
                    {error.error === "invalid" && (
                        <span>
                            Invalid prop <Var>{error.name}</Var> set on{" "}
                            <Tag>{tag_name}</Tag>. Expected{" "}
                            <Type>{error.expected}</Type>, got{" "}
                            <Type>{error.actual}</Type>.
                        </span>
                    )}
                    {error.error === "missing" && (
                        <span>
                            Required prop <Var>{error.name}</Var> of type{" "}
                            <Type>{error.expected}</Type> not set on{" "}
                            <Tag>{tag_name}</Tag>.
                        </span>
                    )}
                    {error.error === "extra" && (
                        <span>
                            Extra prop <Var>{error.name}</Var> of type{" "}
                            <Type>{error.actual}</Type> set on{" "}
                            <Tag>{tag_name}</Tag>.
                        </span>
                    )}
                </li>
            ))}
        </ul>
    </div>
);

const ErrorModal = () => {
    const [slippersErrors, setSlippersErrors] = useState<SlippersError[]>([]);
    const [showModal, setShowModal] = useState(false);

    useEffect(() => {
        // setSlippersErrors(window.slippersPropErrors || []);
        // Test errors
        const testErrors = [
            {
                tag_name: "Button",
                template_name: "pattern-library/pages/home_page/home_page.html",
                lineno: 1,
                errors: [
                    {
                        error: "invalid",
                        name: "color",
                        expected: "string",
                        actual: "number",
                    },
                    {
                        error: "missing",
                        name: "size",
                        expected: "string",
                    },
                ],
            },
            {
                tag_name: "CardLink",
                template_name: "pattern-library/pages/home_page/home_page.html",
                lineno: 2,
                errors: [
                    {
                        error: "extra",
                        name: "size",
                        actual: "string",
                    },
                ],
            },
        ];
        setSlippersErrors([].concat(...Array(10).fill(testErrors)));
        setShowModal(true);
    }, []);

    return (
        <>
            {showModal && (
                <div className="absolute inset-0 bg-black/90 text-white p-12 overflow-auto">
                    <div className="flex flex-col">
                        <h1 className="text-2xl text-red-400 mb-8">
                            Slippers: Failed prop types
                        </h1>
                        <div className="space-y-8">
                            {slippersErrors.map((error, i) => (
                                <ErrorBox key={i} error={error} />
                            ))}
                        </div>
                    </div>
                    <button
                        className="absolute right-12 top-12 px-4 py-2 bg-black"
                        onClick={() => setShowModal(false)}
                    >
                        Close
                    </button>
                </div>
            )}
        </>
    );
};

function App() {
    return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="bg-zinc-200 p-20">
                <h1 className="text-5xl font-bold">Hello, World</h1>
            </div>
            <ErrorModal />
        </div>
    );
}

export default App;
