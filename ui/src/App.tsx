import React, { useState, useEffect } from "react";
import { useLockBodyScroll } from "react-use";

declare global {
    interface Window {
        slippersPropErrors: SlippersError[];
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
    <div data-testid="error-box">
        <p>{tag_name}</p>
        <p className="text-zinc-400 font-mono break-words">
            {template_name}:{lineno}
        </p>
        <ul className="mt-4 p-4 bg-zinc-800 text-zinc-200">
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

const ErrorModal = ({ errors }: { errors: SlippersError[] }) => {
    const [showModal, setShowModal] = useState(false);

    useEffect(() => {
        if (errors.length > 0) {
            setShowModal(true);
        }
    }, [errors.length]);

    useLockBodyScroll(showModal);

    return (
        <>
            {showModal && (
                <div className="fixed inset-0 bg-black/90 text-white p-12 overflow-auto">
                    <div className="flex flex-col">
                        <div className="flex items-start">
                            <h1 className="text-2xl text-red-400 mb-8">
                                Slippers: Failed prop types
                            </h1>
                            <button
                                className="ml-auto px-4 py-2 bg-black"
                                onClick={() => setShowModal(false)}
                            >
                                Close
                            </button>
                        </div>
                        <div className="space-y-8">
                            {errors.map((error, i) => (
                                <ErrorBox key={i} error={error} />
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </>
    );
};

function App({ errors }: { errors: SlippersError[] }) {
    return <ErrorModal errors={errors} />;
}

export default App;
