local pickers = require("telescope.pickers")
local finders = require("telescope.finders")
local previewers = require("telescope.previewers")
local actions = require("telescope.actions")
local action_state = require("telescope.actions.state")
local conf = require("telescope.config").values

local M = {}

M.sigma_picker = function(opts)
    opts = opts or {}

    -- Backends for Sigma Rules
    local sigma_rules = {
        "elasticsearch",
        "kibana",
        "splunk",
        "graylog",
    }

    pickers.new(opts, {
        prompt_title = "Sigma Rules Backend Picker",
        finder = finders.new_table({
            results = sigma_rules,
        }),
        sorter = conf.generic_sorter(opts),
        previewer = previewers.new_buffer_previewer({
            define_preview = function(self, entry, status)
                local rule = entry.value
                self.state.bufnr = vim.api.nvim_create_buf(false, true)
                vim.api.nvim_buf_set_lines(self.state.bufnr, 0, -1, false, { "Preview for: " .. rule })
            end,
        }),
        attach_mappings = function(prompt_bufnr, map)
            actions.select_default:replace(function()
                local selection = action_state.get_selected_entry()
                actions.close(prompt_bufnr)

                local selected_backend = selection.value
                local command = "python3 /home/m3lk0r/Desktop/sigma-ls/backend-converter/convert.py " .. selected_backend

                print("Running backend converter for: " .. selected_backend)

                -- Execute the backend converter script
                vim.fn.jobstart(command, {
                    stdout_buffered = true,
                    on_stdout = function(_, data)
                        if data then
                            print("Output:", table.concat(data, "\n"))
                        end
                    end,
                    on_stderr = function(_, data)
                        if data then
                            print("Error:", table.concat(data, "\n"))
                        end
                    end,
                    on_exit = function(_, code)
                        print("Backend converter exited with code:", code)
                    end,
                })
            end)
            return true
        end,
    }):find()
end

M.sigma_picker()
return M

-- Trying to add it as a telescope extension is a pain. Still working on it
-- Export the picker as a Telescope extension
--return require("telescope").register_extension({
--    exports = {
--        sigma_picker = M.sigma_picker,
--    },
--})

