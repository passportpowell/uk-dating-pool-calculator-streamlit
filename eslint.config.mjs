import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import hooks from 'eslint-plugin-react-hooks';
import a11y from 'eslint-plugin-jsx-a11y';
export default tseslint.config(
  {ignores:['.next/**','out/**','build/**','next-env.d.ts','archive/**','scratch/**','docs/**']},
  {files:['src/**/*.ts','src/**/*.tsx'],extends:[js.configs.recommended,...tseslint.configs.recommended],plugins:{'react-hooks':hooks,'jsx-a11y':a11y},rules:{...hooks.configs.recommended.rules,...a11y.flatConfigs.recommended.rules}},
);
