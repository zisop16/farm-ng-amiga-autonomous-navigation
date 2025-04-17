import { createContext, useContext, useState, RefObject } from "react";
import { Modal } from "@mui/material";
import Keyboard from "react-simple-keyboard";
import "react-simple-keyboard/build/css/index.css";

type Setter = (value: string) => void;
type FieldRef = RefObject<HTMLInputElement>;

interface KeyboardContextProps {
  openKeyboard: (updateField: Setter, currentInputValue: string, ref?: FieldRef) => void
}

const KeyboardContext = createContext<KeyboardContextProps>({
  openKeyboard: () => {}
});

export const KeyboardProvider = ({ children }: { children: React.ReactNode }) => {
  const [showKeyboard, setShowKeyboard] = useState(false);
  const [updateInputField, setUpdateInputField] = useState<Setter>(() => () => {});
  const [inputValue,  setInputValue] = useState("");
  const [inputRef, setInputRef] = useState<FieldRef>();

  const openKeyboard = (updateField: Setter, currentInput: string, ref?: FieldRef) => {
    setUpdateInputField(() => updateField); // Update TextField that currently has focus
    setInputValue(currentInput);
    setInputRef(ref);
    setShowKeyboard(true);
  };

  const handleKeyboardInput = (inputValue: string) => {
    setInputValue(inputValue);
    updateInputField(inputValue);
    requestAnimationFrame(() => inputRef?.current?.focus());
  };

  return (
    <KeyboardContext.Provider value={{ openKeyboard }}>
      {children}

      <Modal open={showKeyboard} onClose={() => setShowKeyboard(false)} BackdropProps={{ style: { backgroundColor: "transparent" } }} 
      sx={{
        display: "flex",
        alignItems: "flex-end", 
        justifyContent: "center",
        border: "none",
      }}>
        <Keyboard
          onChange={handleKeyboardInput}
          input={inputValue} 
        />
      </Modal>
    </KeyboardContext.Provider>
  );
};

export const useKeyboard = () => useContext(KeyboardContext);
